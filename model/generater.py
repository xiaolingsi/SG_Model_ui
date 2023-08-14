import io
import sys
from sqlalchemy import create_engine, MetaData
from sqlacodegen.codegen import CodeGenerator
from urllib.parse import quote_plus as urlquote

def generate_model(host, user, password, database, outfile = None):
    engine = create_engine(f'mysql+pymysql://{user}:{urlquote(password)}@{host}/{database}')
    metadata = MetaData(bind=engine)
    metadata.reflect()
    outfile = io.open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.render(outfile)

if __name__ == '__main__':
    generate_model('180.76.100.226:3306', 'admin', 'reju@20220601!', 'lwm', 'model.py')