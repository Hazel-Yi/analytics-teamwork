from Create_db import create_connection, create_table_details

if __name__ == '__main__':
    details_csv = 'games_detailed_info.csv'
    conn = create_connection('Database')
    create_table_details(details_csv, conn)

