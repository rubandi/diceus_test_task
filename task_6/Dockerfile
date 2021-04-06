FROM python:3.8.3

WORKDIR /app

ADD tests/ /app/
RUN pip install selenium pytest

CMD ["pytest", "test.py", "--html=report/pytest_report.html"]