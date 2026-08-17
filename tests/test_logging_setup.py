import logging

import netlab.logging_setup as ls


def test_setup_returns_configured_logger():
    log = ls.setup_logging(module="demo")
    assert isinstance(log, logging.Logger)
    assert log.handlers


def test_logfile_writes_structured_record(tmp_path):
    logfile = tmp_path / "sub" / "run.log"
    log = ls.setup_logging(module="7.3", logfile=logfile)
    log.info("Katz nodes=5 alpha=0.1 done=0.0021s")
    content = logfile.read_text()
    assert "Katz nodes=5 alpha=0.1 done=0.0021s" in content
    assert "7.3" in content