from scheduler import execute

import time
execute('hautelook', 'update_category')
execute('hautelook', 'update_listing')
execute('hautelook', 'update_product')

while True:
    print 'looping'
    time.sleep(10)
