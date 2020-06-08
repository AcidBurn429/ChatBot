"""

CREATE TABLE `database`.`tokens` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `token` VARCHAR(1024) NOT NULL,
  `status` INT NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `token_UNIQUE` (`token` ASC) VISIBLE,
  UNIQUE INDEX `status_UNIQUE` (`status` ASC) VISIBLE);

"""

from hashlib import sha3_512
from os import urandom
from base64 import b64encode
from time import time


class Token:
    def __init__(self, database):
        self.database = database

    def create_token(self):
        token = sha3_512(b64encode(urandom(7000)) + bytes(str(time()), "utf-8")).hexdigest()
        self.database.execute("INSERT INTO tokens (token, status) VALUES (?, 0)", (token,))
        return token

    def check_token(self, token):
        tokens = self.database.execute("SELECT status FROM tokens WHERE token = ?", (token, ), ret=True).fetchall()

        if len(tokens) == 1:
            if tokens[0][0] == 0:
                self.database.execute("UPDATE tokens SET status = 1 WHERE token = ?", (token, ))

                return True
            else:
                return False
        else:
            return False
