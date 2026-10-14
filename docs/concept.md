

# Архитектура торговой системы

## Основные компоненты

1. **Datafeed** — поставляет рыночные данные (historical / live / on-demand).
2. **Strategy** — принимает торговые решения и определяет целевые позиции.
3. **Order Processor** — преобразует решения стратегии в заявки и управляет их исполнением.
4. **Accounting** — ведёт учёт денег, сделок и позиций.
5. **Performance Reporter** — рассчитывает результаты торговли и показатели эффективности.

## Принципы архитектуры

- **Единая архитектура** для backtesting, simulation и live trading.
- **Accounting → Strategy** — стратегия получает информацию о текущем состоянии портфеля из Accounting.
- **Accounting → Performance Reporter** — отчётность строится на основе данных учёта.
- **Datafeed → Performance Reporter** — рыночные данные используются для оценки портфеля и расчёта показателей эффективности.
- **Order Processor** поддерживает два режима исполнения: симуляция и реальная торговля через брокера или биржу.

## Общая схема

```text
                Datafeed
                   |
                   v
                Strategy <------------+
                   |                  |
             Target Positions         |
                   |                  |
                   v                  |
            Order Processor           |
              /         \             |
             v           v            |
        Simulator    Broker/Exchange   |
             \           /            |
              v         v             |
                Accounting -----------+
                    |
                    v
            Performance Reporter
```

## Открытые вопросы

1. Является ли Accounting единственным источником информации о текущем портфеле?
2. Какие данные Performance Reporter получает непосредственно из Datafeed?