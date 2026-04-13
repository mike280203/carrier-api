"""Funktionen für E-Mails."""

from email.mime.text import MIMEText
from email.utils import make_msgid
from smtplib import SMTP, SMTPServerDisconnected
from socket import gaierror
from typing import Final
from uuid import uuid4

from loguru import logger

from carrier.config import (
    mail_enabled,
    mail_host,
    mail_port,
    mail_timeout,
)
from carrier.service.carrier_dto import CarrierDTO

__all__ = ["send_mail"]

MAILSERVER: Final = mail_host
PORT: Final = mail_port
SENDER: Final = "Python Server <python.server@acme.com>"
RECEIVERS: Final = ["Buchhaltung <buchhaltung@acme.com>"]
TIMEOUT: Final = mail_timeout


def send_mail(carrier_dto: CarrierDTO) -> None:
    """Funktion, um eine E-Mail zu senden."""
    logger.debug("{}", carrier_dto)
    if not mail_enabled:
        logger.warning("send_mail: Der Mailserver ist deaktiviert")
        return

    msg: Final = MIMEText(f"Neuer Carrier: <b>{carrier_dto.name}</b>")
    msg["Subject"] = f"Neuer Carrier: ID={carrier_dto.id}"
    msg["Message-ID"] = make_msgid(idstring=str(uuid4()))

    try:
        logger.debug("mailserver={}, port={}", MAILSERVER, PORT)
        with SMTP(host=MAILSERVER, port=PORT, timeout=TIMEOUT) as smtp:
            smtp.sendmail(from_addr=SENDER, to_addrs=RECEIVERS, msg=msg.as_string())
            logger.debug("msg={}", msg)
    except ConnectionRefusedError:
        logger.warning("ConnectionRefusedError")
    except SMTPServerDisconnected:
        logger.warning("SMTPServerDisconnected")
    except gaierror:
        logger.warning("socket.gaierror: Laeuft der Mailserver im virtuellen Netzwerk?")
