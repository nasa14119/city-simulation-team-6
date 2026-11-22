from threading import Thread

import router
from hello import main

if __name__ == "__main__":
    api = Thread(target=router.server, daemon=True)
    api.start()
    main()
