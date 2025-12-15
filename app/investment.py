import pandas as pd
from datetime import datetime


def simulate_investment(df: pd.DataFrame) -> None:
    """
    Recebe o DataFrame com coluna 'Adj Close' e
    pergunta valor investido e data de compra,
    mostrando lucro/prejuízo e retorno percentual.
    """
    print("\n=== Simulação de Investimento ===")
    invested_str = input("Valor investido em USD (ex: 1000): ").strip()
    buy_date_str = input("Data de compra (AAAA-MM-DD) [vazio = primeira data]: ").strip()

    # Trata valor investido
    try:
        invested = float(invested_str)
    except ValueError:
        print("Valor inválido, usando 1000 USD.")
        invested = 1000.0

    # Garante que o índice é datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        df = df.copy()
        df.index = pd.to_datetime(df.index)

    # Descobre preço de compra
    if buy_date_str:
        try:
            buy_date = datetime.strptime(buy_date_str, "%Y-%m-%d")
            buy_ts = pd.Timestamp(buy_date)
            # Filtra primeira data >= buy_date
            df_buy = df[df.index >= buy_ts]
            if df_buy.empty:
                print("Não há dados a partir dessa data, usando primeira data disponível.")
                buy_price = df["Adj Close"].iloc[0]
            else:
                buy_price = df_buy["Adj Close"].iloc[0]
        except ValueError:
            print("Data inválida, usando primeira data disponível.")
            buy_price = df["Adj Close"].iloc[0]
    else:
        buy_price = df["Adj Close"].iloc[0]

    # Cálculos principais
    current_price = df["Adj Close"].iloc[-1]
    coins = invested / buy_price
    current_value = coins * current_price
    profit = current_value - invested
    profit_pct = (profit / invested) * 100

    print("\n=== Resultado do Investimento ===")
    print(f"Preço na compra:       {buy_price:.4f} USD")
    print(f"Preço atual:           {current_price:.4f} USD")
    print(f"Quantidade de moedas:  {coins:.6f}")
    print(f"Valor atual:           {current_value:.2f} USD")
    print(f"Lucro/Prejuízo:        {profit:.2f} USD ({profit_pct:.2f}%)")
