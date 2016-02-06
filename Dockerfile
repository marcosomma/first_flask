FROM python:2.7
RUN pip install -r requirements.txt
# ADD main.py .
EXPOSE 5000
CMD python main.py
