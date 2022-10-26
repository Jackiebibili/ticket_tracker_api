from .. import constants
from ..models.pick import Pick
import typing, threading
from .util.decorators import StorageInsertionOrder, wrap_fn_return
from .strategies.quarters_seats import QuartersSeats
from ..schedulers.mail_scheduler import mail_scheduler


def run_async_tasks(picks: typing.Iterable[Pick], scraping_id: str, target_price: int, emails: list[str]):
    picks_size = len(list(picks))
    if picks_size == 0: return

    store = StorageInsertionOrder(size=picks_size)
    def fn(arg: tuple[int, Pick]):
        idx, pick = arg
        thread = threading.Thread(target=wrap_fn_return(run_async_task, store.set, idx), args=(pick, scraping_id, target_price))
        thread.start()
        return thread

    threads = list(map(fn, enumerate(picks)))

    for thread in threads: thread.join()

    # filter out new seats that do not need alerts
    store.filter()
    # better seats first
    store.sort()
    # get seats used in alerting
    alert_seats = store.sublist(0, min(store.size, constants.ALERT_SEATS_MAX_COUNT))
    # get the alert information
    alert_contents = list(map(lambda qs: qs.get_alert_content(), alert_seats))  # type: ignore
    # send the alert to user
    mail_scheduler.send(emails, alert_contents)


def run_async_task(pick: Pick, scraping_id: str, target_price: int):
    # Alert the user based on alert conditions
    qs = QuartersSeats(pick, scraping_id, target_price)
    if not qs.shouldAlert():
        return None

    # success
    return qs
