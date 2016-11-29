__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

from CHROnIC_Portal import app


app.secret_key = '1234'
app.run(host='0.0.0.0', port=5000, debug=True)
