# find and clean 10-K submissions
def sub_clean(sub_df):
    sub = sub_df.loc[sub_df['form']=='10-K']
    sub = sub.loc[sub[sub['fp']=='FY'].index]
    #if sic is blank, i don't want it!
    sub.drop(sub.loc[sub['sic'].isna()].index,axis=0,inplace=True)

    # change fye column to a categorical var
    def fy(numbers):
        mapping = {}
        for number in numbers:
            if number < 400:
                mapping[number]= 'Q1'
            if 400 < number < 700:
                mapping[number] = 'Q2'
            if 700 < number < 1000:
                mapping[number] = 'Q3'
            if 1000 < number < 1300:
                mapping[number] = 'Q4'
        return mapping
    sub['FY_end'] = sub['fye'].map(fy(sub['fye']))

    # i don't care about address columns
    # I don't care about EIN because we already have cik
    # 'countryba', biz address country, has the fewest nan values, so we'll keep that and drop the rest
    # aciks stands for additional ciks
        # dropping it because I think these will be represented elsewhere
    # 'former' and 'changed' represent company name changes
        # dropping because i assume that the cik remains consistent
        # we'll use current names associated with cik for analysis
    # dropping filing and accepted date because they don't mean much to me

    unwanted_columns = [
        'stprba', 'cityba', 'zipba',
        'bas1', 'bas2', 'baph',
        'stprma', 'cityma', 'zipma',
        'mas1', 'mas2','stprinc','ein',
        'afs','wksi','fye','countryma',
        'countryinc','aciks','changed',
        'former','fp','filed','accepted']
    sub.drop(columns=unwanted_columns,inplace=True)

    return sub

GAAP_tags = all_tags[all_tags['version'].str.contains('gaap')]
non_abstract_GAAP_tags = GAAP_tags[GAAP_tags['abstract']==0]['tag']
parsed_nums = all_nums[all_nums['tag'].isin(non_abstract_GAAP_tags)]

pivot = parsed_nums.pivot_table(index='adsh',columns='tag',values='value')
parsed_pivot = pivot[pivot.notna().sum().sort_values(ascending=False)[:10].index].dropna()

def get_Acc_num(symbol,form_type):
    url = f"""https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={symbol}&type={form_type}&dateb=&owner=exclude&count=40"""

    page = BeautifulSoup(requests.get(url).content)

    data_buttons = page.find_all(attrs={'id':'interactiveDataBtn'})

    viewers = [x['href'] for x in data_buttons]

    return [x.split('accession_number=')[1][:20].replace('-','') for x in viewers]
MSFT_10Ks = get_Acc_num('MSFT','10-K')
income_stmts = [sec.get_incomeStatement('0000789019',x) for x in MSFT_10Ks]
income_dfs = [pd.DataFrame(x) for x in income_stmts]

pd.read_excel('https://www.sec.gov/Archives/edgar/data/789019/000156459019027952/Financial_Report.xlsx',sheet_name=1)

def continue_inserting(filename,db,table):
    data = pd.read_csv(filename,
                        sep='\t',
                        lineterminator='\n',
                        header=0)

    # these are the primary keys according to the data dictionary. yuck.
    if 'pre.txt' in filename:
        data['pk'] = (data['adsh']+
               data['report'].astype('str')+
               data['line'].astype('str')
              )
        key='pk'
    elif 'num.txt' in filename:
        data['pk']= (data['adsh']+data['tag']+
              data['version']+
              data['ddate'].astype('str')+
              data['qtrs'].astype('str')+
              data['uom']+data['coreg'].fillna(''))
        key='pk'
    elif 'tag.txt' in filename:
        data['pk'] = data['tag']+data['version']
        key='pk'

    else:
        key = 'adsh'

    already_inserted = db.query_to_df(f"""select * from {db.DB_name}.{table};""")

    not_inserted = data[~data[key].isin(already_inserted[key])]

    print(data.shape,not_inserted.shape)

    db.insert_fromDf_iteration(not_inserted.fillna('NULL'),table)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String,Date,Boolean,DateTime

class Submission(Base):
    __tablename__ = 'submissions'

    adsh = Column(String,primary_key=True)
    cik = Column(Integer)
    name = Column(String)
    sic = Column(Integer)
    countryba = Column(String)
    stprba = Column(String)
    cityba = Column(String)
    zipba = Column(String)
    bas1 = Column(String)
    bas2 = Column(String)
    baphb = Column(String)
    countryma = Column(String)
    stprma = Column(String)
    cityma = Column(String)
    zipma = Column(String)
    mas1 = Column(String)
    mas2 = Column(String)
    countryinc = Column(String)
    stprinc = Column(String)
    ein = Column(Integer)
    former = Column(String)
    changed = Column(String)
    afs = Column(String)
    wksi = Column(Boolean)
    fye = Column(String)
    form = Column(String)
    period=Column(Date)
    fy = Column(Date)
    fp = Column(String)
    filed = Column(Date)
    accepted = Column(DateTime)
    prevrpt = Column(Boolean)
    detail = Column(Boolean)
    instance = Column(String)
    nciks = Column(Integer)
    aciks = Column(String)

    def __repr__(self):
        return "<submission(name='%s', form='%s', fp='%s')>" % (
                 self.name, self.form, self.fp
        )

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db)
session = Session()
session.bulk_insert_mappings(Submission, df.to_dict(orient="records"))
session.close()

def alchemy_insert(db,data,table_name,exists_behavior):
#     already_inserted = pd.read_sql(table_name,db)

#     key = 'adsh'

#     not_inserted = data[~data[key].isin(already_inserted[key])]

    data.to_sql(table_name,db,if_exists=exists_behavior,index=False)

def remove_zeros(cik):
    if cik.startswith('0')==False:
        return cik
    else:
        cik=cik[1:]
    return remove_zeros(cik)

df['index']=df['index'].map(lambda x: remove_zeros(x))