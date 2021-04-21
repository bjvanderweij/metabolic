"""Script for loading initialization data."""

import asyncio
import csv
import logging
import sys
import typing as T
from contextlib import contextmanager

import typer
from bson.objectid import ObjectId  # type: ignore

import util
import settings

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@contextmanager
def csv_data_reader(path: str):
    with open(path) as f:
        yield csv.reader(f)


async def insert_indicators(path: str) -> T.List[ObjectId]:
    """Read the first two rows of the data at path and construct
    and insert indicator data.

    Return a list of MongoDB IDs corresponding to indicators in
    the order in which they appear in the header.
    """
    db = util.get_mongo_client()
    indicator_ids = []
    with csv_data_reader(path) as reader:
        indicator_strs = next(reader)[5:]
        unit = next(reader)[5:]
        for indicator_str, unit in zip(indicator_strs, unit):
            try:
                method, category, name = indicator_str.split(':')
            except ValueError:
                logger.warning(
                        f'skipping indicator string {indicator_str}')
                continue
            indicator = {
                    'method': method,
                    'category': category,
                    'name': name,
                    'unit': unit
                }
            result = await db.rivm2016.indicator.insert_one(indicator)
            indicator_ids.append(result.inserted_id)
    return indicator_ids


async def insert_geographies() -> T.Dict[str, ObjectId]:
    """Placeholder function for loading geography data.

    Return a dictionary mapping geography short names to
    MongoDB IDs."""
    geographies = [
            {
                'short_name': 'NL',
                'name': 'The Netherlands'
            }
        ]
    db = util.get_mongo_client()
    id_table: T.Dict[str, ObjectId] = {}
    for geography in geographies:
        result = await db.rivm2016.geography.insert_one(geography)
        id_table[geography['short_name']] = result.inserted_id
    return id_table


async def insert_entries_and_impacts(
            path: str,
            indicator_ids: T.List[ObjectId],
            geography_table: T.Dict[str, ObjectId]
        ) -> None:
    """Read data from path and construct and insert entries and
    impacts.
    """
    rows, skipped = 0, 0
    db = util.get_mongo_client()
    with csv_data_reader(path) as reader:
        # Skip the first two rows
        next(reader)
        next(reader)
        for row in reader:
            rows += 1
            _, ecoinvent_str, unit, _, _, *indicator_values = row
            try:
                # product_name, sub_type, geography, method, data_source = (
                # ecoinvent_str.split(','))
                product_name, geography, _, _ = ecoinvent_str.strip().split(
                        ',')
                geography = geography.strip()[1:-1]
            except ValueError:
                skipped += 1
                logger.warning(f'skipping ecoinvent string {ecoinvent_str}')
                continue
            entry = {
                'product_name': product_name,
                'geography_id': geography_table[geography],
                'unit': unit
            }
            entry_result = await db.rivm2016.entry.insert_one(entry)
            for coeff, indicator_id in zip(indicator_values, indicator_ids):
                if coeff == '':
                    continue
                impact = {
                        'indicator_id': indicator_id,
                        'entry_id': entry_result.inserted_id,
                        'coefficient': float(coeff)
                    }
                await db.rivm2016.impact.insert_one(impact)
    logger.warning(f'skipped {skipped}/{rows}')


COLLECTIONS = ['entry', 'indicator', 'geography', 'impact']


async def load_data(
        data_path,
        force,
        mongodb_host,
        mongodb_port,
        ) -> None:
    db = util.get_mongo_client(host=mongodb_host, port=mongodb_port)
    if await db.main.initialized.find_one() is None or force:
        logger.info('initializing database')
        for collection in COLLECTIONS:
            logger.info(f'deleting {collection}')
            await db.rivm2016[collection].delete_many({})
        try:
            geographies_id_table = await insert_geographies()
            indicator_ids = await insert_indicators(data_path)
            await insert_entries_and_impacts(
                    data_path,
                    indicator_ids,
                    geographies_id_table,
                )
            # Insert an arbitrary bit of information to mark
            # initialization as done
            await db.main.initialized.update_one({'done': True}, upsert=True)
        except Exception as exc:
            raise type(exc)(
                    f'encountered {str(exc)} while initializing database'
                ).with_traceback(sys.exc_info()[2])
    else:
        logger.info('skipping initialization (database already initialized)')


def main(
        data_path: str = settings.DATA_PATH,
        force: bool = False,
        mongodb_host: str = settings.MONGODB_HOST,
        mongodb_port: int = settings.MONGODB_PORT
        ) -> None:
    """Initialize the database.

    If the database has not been initialized, existing data will be
    deleted and new data inserted.

    Keyword arguments:
    data_path -- path to CSV data
    force -- if True, the script will run independent of whether the
        database has already been initialized (default: False)
    """
    asyncio.run(load_data(data_path, force, mongodb_host, mongodb_port))


if __name__ == '__main__':
    typer.run(main)
