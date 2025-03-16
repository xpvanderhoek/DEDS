import pandas as pd
from settings import settings
from data_processing import load_tables, vraag5, vraag6, vraag7, vraag8, vraag9

def process():

    results = {
        'vraag5': vraag5(load_tables('retailer_site')),
        'vraag6': vraag6(load_tables('country')),
        'vraag7': vraag7(load_tables('sales_branch')),
        'vraag8': pd.DataFrame({'Aantal Teruggebracht': [vraag8(load_tables('returned_item'))]}),
        'vraag9': pd.DataFrame({'Verkoopafdelingen met Regio': [vraag9(load_tables('sales_branch'))]})
    }

    output_dir = settings.processeddir
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, df in results.items():
        df.to_excel(output_dir / f"{name}.xlsx", index=False)