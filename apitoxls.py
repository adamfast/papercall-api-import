from requests import get
import xlwt

# Possible proposal states
PROPOSAL_STATES = ('submitted', 'accepted', 'rejected', 'waitlist')

# Style for the Spreadsheet headers
HEADER_STYLE = xlwt.easyxf(
    'font: name Verdana, color-index blue, bold on',
    num_format_str='#,##0.00'
)

# Get the user's API key
print('Your DjangoCon PaperCall API Key can be found here: https://www.papercall.io/events/316/apidocs')
API_KEY = input('Please enter your PaperCall event API Key: ')
if len(API_KEY) != 32:
    raise ValueError('Error: API Key must be 32 characters long.')

# Get destination file name
DEST_FILE = input('Filename to write [djangoconus.xls]: ') or 'djangoconus.xls'

# Create the Spreadsheet Workbook
wb = xlwt.Workbook()

for ps in PROPOSAL_STATES:
    # Reset row counter for the new sheet
    # Row 0 is reserved for the header
    num_row = 1

    # Create the new sheet and header row for each talk state
    ws = wb.add_sheet(ps.upper())
    ws.write(0, 0, 'ID', HEADER_STYLE)
    ws.write(0, 1, 'Title', HEADER_STYLE)
    ws.write(0, 2, 'Format', HEADER_STYLE)
    ws.write(0, 3, 'Audience', HEADER_STYLE)
    ws.write(0, 4, 'Rating', HEADER_STYLE)

    r = get(
        'https://www.papercall.io/api/v1/submissions?_token={0}&state={1}'.format(
            API_KEY,
            ps,
        )
    )

    for proposal in r.json():
        ws.write(num_row, 0, proposal['id'])
        ws.write(num_row, 1, proposal['talk']['title'])
        ws.write(num_row, 2, proposal['talk']['talk_format'])
        ws.write(num_row, 3, proposal['talk']['audience_level'])
        ws.write(num_row, 4, proposal['rating'])

        num_row += 1

wb.save(DEST_FILE)
print('Complete!')
