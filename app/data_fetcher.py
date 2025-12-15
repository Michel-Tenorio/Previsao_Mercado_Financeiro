import requests
import pandas as pd
from pandas import DataFrame
from typing import Optional


def get_history(
    coin_id: str, days: int = 365, vs_currency: str = "usd"
) -> DataFrame:
    """
    Busca histórico diário de uma cripto na CoinGecko.

    coin_id exemplos: 'bitcoin', 'ethereum'
    days: número de dias de histórico (ex: 30, 90, 365, 1825)
    """
    url = (
        f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        f"?vs_currency={vs_currency}&days={days}&interval=daily"
    )

    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        raise ValueError(
            f"Erro ao buscar dados na CoinGecko ({resp.status_code})."
        )

    data = resp.json()

    if "prices" not in data or not data["prices"]:
        raise ValueError(f"Nenhum dado de preço encontrado para {coin_id}.")

    # CoinGecko retorna [timestamp_ms, price]
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("Date", inplace=True)
    df.drop(columns=["timestamp"], inplace=True)

    # Adapta para o restante do código (usa 'Adj Close')
    df.rename(columns={"price": "Adj Close"}, inplace=True)

    return df
