import os
from cloud_app import create_app

app = create_app()

# true if we run this script directly
if __name__ == '__main__':
	app.run(debug=True)
