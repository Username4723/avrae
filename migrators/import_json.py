import asyncio
import json
import os
import sys

sys.path.append('..')

import motor.motor_asyncio

LOAD_FILES = {
    'names': [],
    'srd-backgrounds': [],
    'srd-bestiary': [],
    'srd-classfeats': [],
    'srd-classes': [],
    'srd-feats': [],
    'srd-items': [],
    'srd-races': [],
    'srd-spells': [],
    'srd-references': [],

    'itemprops': {},
    'nsrd-names': {},
}


async def run(mdb):
    for basename, default in LOAD_FILES.items():
        data = default
        filepath = os.path.join('..', 'res', f'{basename}.json')
        try:
            with open(filepath, 'r')as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f'File not found: {filepath}; skipping import')
            continue

#        for i in range(len(data)): data[i].srd = True

        print(f'Inserting {len(data)} items for {basename}...', flush=True)
        result = await mdb.static_data.update_one(
            {'key': basename},
            {'$set': {'object': data}},
            upsert=True
        )
        print(result)
    print('Creating index on static_data...', end=' ', flush=True)
    await mdb.static_data.create_index("key", unique=True)
    print('done.')


if __name__ == '__main__':
    mdb = None
    if 'test' in sys.argv:
        import credentials

        mdb = motor.motor_asyncio.AsyncIOMotorClient(credentials.test_mongo_url).avrae
    else:
        mclient = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_URL', "mongodb://localhost:27017"))
        mdb = mclient[os.getenv('MONGO_DB', "avrae")]

    input(f"Inserting into {mdb.name}. Press enter to continue.")
    asyncio.get_event_loop().run_until_complete(run(mdb))
