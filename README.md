
# ItemLocator App

**This console application is capable of 
locating warehouse items from given 
orders and grouping them by the corresponding racks**

## 💪Built with
![Static Badge](https://img.shields.io/badge/Python-1?style=flat&logo=Python&labelColor=ffd847&color=3776ab&link=https%3A%2F%2Fwww.python.org%2F)
![Static Badge](https://img.shields.io/badge/PostgreSQL-1?style=flat&logo=PostgreSQL&labelColor=ffffff&color=336791&link=https%3A%2F%2Fwww.postgresql.org%2F)

## ✨Give it a try

*Expected to use **Bash** or similar shell alternatives*

*Expected that user already have **populated PostgreSQL database** with corresponding schema*

<br>

clone repo >> generate .env >> edit it

```bash
git clone https://github.com/Kimoi/ItemLocator-App.git && \
cd ItemLocator-App && \
cp env_example .env && \
nano .env
```

<br>

Activate venv Linux / macOS

`python -m venv venv && source venv/bin/activate`

Activate venv Windows

`python -m venv venv && source venv/Scripts/activate`

<br>

Install requirements

```bash
python -m pip install --upgrade pip && \
pip install -r requirements.txt
```

## ⚡Database schema

![sch](./media/sch.png)

## 🪄Usage example

Type

`python main.py 10,11,14,15`

Get

![res](./media/res.png)

## ⚠️Erase project

`deactivate && cd .. && rm -fr ItemLocator-App`
