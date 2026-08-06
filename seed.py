import asyncio
from database import engine, Base, async_session_factory
from models import Account, Client

async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        c1 = Client(full_name='Петр Петров', email='1@mail.com')
        c2 = Client(full_name='Василий Васильев', email='2@mail.com')
        c3 = Client(full_name='Иван Иванов', email='3@mail.com')
        session.add_all([c1, c2, c3])
        await session.flush()


        a1 = Account(account_numder='54826971503624875925', client_id=c1.id, balance=1542.3)
        a2 = Account(account_numder='78541021009658745198', client_id=c1.id, balance=4587.3)
        a3 = Account(account_numder='44789658215066397485', client_id=c2.id, balance=6987.6)
        a4 = Account(account_numder='56987596301458726304', clent_id=c3.id, balance=475.2, is_active=False)
        session.add_all([a1, a2, a3, a4])
        await session.commit()
        print('БД инициализирована')

if __name__ == '__main__':
    asyncio.run(seed_data())