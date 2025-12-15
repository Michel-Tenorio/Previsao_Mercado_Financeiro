import matplotlib.pyplot as plt
from app.data_fetcher import get_history
from app.analysis import add_indicators, summarize
from app.investment import simulate_investment


def main():
    print("=== Análise de Criptomoedas ===")
    coin_id = input("Digite o ID da moeda (ex: bitcoin, ethereum): ").strip().lower()
    days_str = input("Quantos dias de histórico deseja analisar? (ex: 30): ").strip()

    try:
        days = int(days_str)
    except ValueError:
        print("Número de dias inválido. Use um inteiro, por exemplo 30.")
        return

    # Buscar dados históricos
    df = get_history(coin_id, days=days)
    print(df.head())
    print("Moeda usada na chamada:", coin_id)
    if df is None or df.empty:
        print("Não foi possível obter dados para essa moeda/período.")
        return

    # Calcular indicadores
    df = add_indicators(df)
    stats = summarize(df)

    # Preço inicial e atual do período
    first_price = df["Adj Close"].iloc[0]
    current_price = df["Adj Close"].iloc[-1]

    print("\n=== Informações do Ativo ===")
    print(f"Moeda:                 {coin_id}")
    print(f"Período analisado:     últimos {days} dias")
    print(f"Preço inicial período: {first_price:.4f} USD")
    print(f"Preço atual:           {current_price:.4f} USD")

    print("\n=== Estatísticas Básicas ===")
    print(f"Retorno total no período: {stats['total_return']*100:.2f}%")
    print(f"Retorno médio diário:    {stats['avg_daily_return']*100:.3f}%")
    print(f"Volatilidade diária:     {stats['daily_volatility']*100:.3f}%")

    # Simulação de investimento (igual ao primeiro projeto)
    simulate_investment(df)

    # Gráfico de preço + médias móveis
    print("\nGerando gráfico...")
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["Adj Close"], label="Preço (USD)")
    if "MA20" in df.columns:
        plt.plot(df.index, df["MA20"], label="Média Móvel 20d")
    if "MA50" in df.columns:
        plt.plot(df.index, df["MA50"], label="Média Móvel 50d")
    plt.title(f"{coin_id.capitalize()} - Preço e Médias Móveis (últimos {days} dias)")
    plt.xlabel("Data")
    plt.ylabel("Preço em USD")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
