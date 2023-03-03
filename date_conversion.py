from datetime import datetime,timezone

def convert_date():
    date_convert = datetime.now(timezone.utc).isoformat().replace('+00.00','')
    da = str(date_convert).split('.')[0]
    return da