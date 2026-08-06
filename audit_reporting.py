import sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from models import Client, Account, TransactionHistory

async def generate_audit_report(
        session: AsyncSession,
        client_id: int
):
    stmt = select(Client).where(Client.c.id == client_id).options(selectinload(Client.accounts))
    res = await session.execute(stmt)
    client = res.scalar_one_or_none()
    if not client:
        print(f'Client с ID {client_id} not found')
        return

    total_balance = sum(acc.balance for acc in client.accounts)
    account_ids = [acc.id for acc in client.accounts]
    tx_stmt = (select(TransactionHistory).where(or_(TransactionHistory.sender_account_id.in_(account_ids), TransactionHistory.receiver_account_id.in_(account_ids)).order_by(TransactionHistory.timestamp.desc()).limit(5)))
    tx_res = await session.execute(tx_stmt)
    recent_trans = tx_res.scalars().all()
    print('-'*60)
    print(f'Отчёт аудита клиента {client.full_name}')
    print('-'*60)
    print('Счета клиента:')
    for acc in client.accounts:
        status_str = "Активен" if acc.is_active else "Заблокирован"
        print(f" -№{acc.account_number} | Баланс: {acc.balance} | Статус: {status_str}")
    print(f'\nСуммарный баланс: {total_balance}')
    print('-'*60)
    print('Последние 5 операций:')
    if not recent_trans:
        print(' Операции отсутствуют.')
    else:
        for tx in recent_trans:
            print(f' [{tx.timestamp.strftime("%Y-%m-%d %H:%M:%S")}]'
                  f'ID: {tx.id} | Отправитель ID: {tx.sender_account_id}'
                  f' ->Получатель ID: {tx.receiver_account_id}'
                  f'Сумма: {tx.amount} | Статус: {tx.status}'
                  f'Инфо: {tx.description}'
                  )
    print('-'*60)
