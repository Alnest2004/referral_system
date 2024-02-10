# syntax=docker/dockerfile:1
FROM python:3.12
LABEL authors="alexander"

WORKDIR /Users/alexander/referral_system

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt /Users/alexander/referral_system/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -Ur requirements.txt
COPY referral_system /Users/alexander/referral_system
