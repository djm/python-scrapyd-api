from scrapyd_api.exceptions import ScrapydError


def test_scrapyd_error():
    err = ScrapydError()
    assert repr(err) == 'ScrapydError("Scrapyd Error")'
    err_with_detail = ScrapydError(detail='Something went wrong')
    assert repr(err_with_detail) == 'ScrapydError("Something went wrong")'
