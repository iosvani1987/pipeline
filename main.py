# pylint: disable=unused-import
import argparse
from asyncio.log import logger
import logging
logging.basicConfig(level=logging.INFO)

import pandas as pd

from metrobus import Metrobus
from base import Base, Session, engine

logger = logging.getLogger(__name__)

def main(filename):
    '''
    This is the main function.
    '''
    print("Hola")
    logging.info('Starting the program')
    logging.info('Reading the file')

    df = pd.read_csv(filename)
    logging.info('Creating the database')
    Base.metadata.create_all(engine)
    logging.info('Creating the session')
    session = Session()
    logging.info('Creating the metrobus objects')

    metrobus_objects = []
    for _, row in df.iterrows():
        metrobus_objects.append(Metrobus(row['vehicle_id'], row['vehicle_label'], row['vehicle_current_status'], row['position_latitude'], row['position_longitude'], row['county']))
        if session.query(Metrobus).filter(Metrobus.vehicle_id == row['vehicle_id']).first() is None:
            logging.info(f"Inserting the metrobus objects {row['vehicle_id']}")
            session.add(Metrobus(row['vehicle_id'], row['vehicle_label'], row['vehicle_current_status'], row['position_latitude'], row['position_longitude'], row['county']))
    
    logging.info('Finishing data base insertion')
    # session.add_all(metrobus_objects)
    logging.info('Committing the changes')
    session.commit()
    logging.info('Finishing the program')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape metrobus data')
    # parser.add_argument('--limit', '-l', type=int, help='limit the number of results')
    # parser.add_argument('--output', '-o', type=str, help='output file')
    parser.add_argument('filename', help='The file you want to load into the DB', type=str)
    args = parser.parse_args()

    main(args.filename)
