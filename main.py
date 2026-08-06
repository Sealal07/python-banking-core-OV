import asyncio
from database import async_session_factory
from seed import seed_data
from services import transfer_funds
from audit_reporting import generate_audit_report

async def main():
    await seed_data()
    async with async_session_factory() as session:
        print('\nЗапуск тестовых сценариев')
        print('Успешный перевод')
        res1 = await transfer_funds(session, sender_account_id=1,
                                    receiver_account_id=3,
                                    amount=5200.0)
        print(f'{"Успех" if res1 else "Ошибка"}\n')
        print('Недостаточно средств')
        res2 = await transfer_funds(session, sender_account_id=2,
                                    receiver_account_id=1
                                    amount=52000.0)
        print(f'{"Успех" if res1 else "Ошибка"}\n')
        print('Заблокированный счет')
        res3 = await transfer_funds(session, sender_account_id=1,
                                    receiver_account_id=4,
                                    amount=520.2)
        print(f'{"Успех" if res1 else "Ошибка"}\n')
        await generate_audit_report(session, client_id=1)
if __name__ == '__main__':
    asyncio.run(main())