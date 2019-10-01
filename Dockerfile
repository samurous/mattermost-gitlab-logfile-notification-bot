FROM python:3.6-stretch

# Set build directory
WORKDIR /tmp

# Install dependencies
RUN pip install requests

WORKDIR /bot

ENTRYPOINT ["python"]
CMD ["bot.py"]
