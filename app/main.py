# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 18:08:32 2023

@author: r.osipovskiy
"""
from dotenv import dotenv_values
import time
import requests
import logging

from parser import TaskScrapper

env = dotenv_values(".env")
scaper = TaskScrapper(env['YOUTRACK_TOKEN'],
                      env['URL'],
                      env['PROJECT'])

# получение пользовательского логгера и установка уровня логирования
py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)
# настройка обработчика и форматировщика в соответствии с нашими нуждами
py_handler = logging.FileHandler("logfile.log" , mode="a+") # f"{__name__}.log", mode='w')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
# добавление форматировщика к обработчику
py_handler.setFormatter(py_formatter)
# добавление обработчика к логгеру
py_logger.addHandler(py_handler)


def main(scrapy, token, chat_id, sleep_time, dbg_cht_id, logger):
    while True:
        status, msg = scrapy.make_step()
        if status and msg == 'ok':
            logger.info(f"INFO: len changes {len(scrapy.changes)}")
            try:
                r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                    json={"chat_id": dbg_cht_id,
                                    "text": f"INFO: len changes {len(scrapy.changes)}" })
            except Exception as e:
                logger.error(f"ERROR in dbg cht id: {e}")

            for _ in range(len(scrapy.changes)):
                message = scrapy.get_value()
                try:
                    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                      json={"chat_id": chat_id,
                                      "parse_mode": 'Markdown',
                                      "text": message}
                                      )

                    if r.status_code != 200:
                        logger.warning("ERROR: status_code != 200 : ", r.content.decode(), message)
                        try:
                            r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                    json={"chat_id": dbg_cht_id,
                                    "text": f"ERROR: status_code != 200:\n {r.content.decode()} \n {message}" })
                        except Exception as e:
                            logger.error(f"ERROR in dbg cht id: {e}")

                except Exception as e:
                    logger.error(f"ERROR: {e}")

        elif msg == 'ok':
            logger.info(f"INFO: len changes {len(scrapy.changes)}")
            try:
                r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                    json={"chat_id": dbg_cht_id,
                                    "text": f"INFO: : len changes {len(scrapy.changes)}, state {len(scrapy.state)}" })
            except Exception as e:
                logger.error(f"ERROR in dbg cht id: {e}")

        else:
            try:
                error_msg = msg.content.decode()
                logger.info("ERROR: in youtrack responce: " + str(error_msg))
                try:
                    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                        json={"chat_id": dbg_cht_id,
                                        "text": f"ERROR: in youtrack responce: {error_msg}" })
                except Exception as e:
                    logger.error(f"ERROR in dbg cht id: {e}")

            except AttributeError:
                logger.info("ERROR: in json.loads of responce: " + str(msg))
                try:
                    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                    json={"chat_id": dbg_cht_id,
                                    "text": f"ERROR: in json.loads of responce: {msg}" })
                except Exception as e:
                    logger.error(f"ERROR in dbg cht id: {e}")

        time.sleep(sleep_time)

if __name__ == "__main__":
    main(scaper, env['TELEGRAM_TOKEN'], env['CHAT_ID'], int(env['SLEEP']), env["DEBUG_CHATID"], py_logger)
