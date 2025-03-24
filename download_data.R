library(dplyr)
library(tidyr)
library(owidapi)
library(wbwdi)
library(ggplot2)
library(readr)

entities <- wdi_get_entities()

# trade_raw <- owid_get("trade-as-share-of-gdp")
# gov_spending_raw <- owid_get("historical-gov-spending-gdp")
gdp_per_capita_raw <- owid_get("gdp-per-capita-worldbank")


# gdp_per_capita_raw |>
#     filter(year == 2022) |>
#     select(entity_id, gdp_per_capita = ny_gdp_pcap_pp_kd) |>
#     left_join(
#         gov_spending_raw |>
#             filter(year == 2022) |>
#             mutate(gov_exp = expenditure / 100) |>
#             select(entity_id, gov_exp),
#         join_by(entity_id)
#     )

gdp_per_capita_raw <- wdi_get(
    "all",
    "NY.GDP.PCAP.CD",
    start_year = 2019,
    end_year = 2019
)

# https://www.who.int/data/gho/data/indicators/indicator-details/GHO/alcohol-attributable-fractions-all-cause-deaths-(-)
fraction_raw <- readr::read_csv("data.csv")

fraction <- fraction_raw |>
    filter(Period == 2019 & Dim2 == "All age groups (total)") |>
    select(
        entity_id = SpatialDimValueCode,
        sex = Dim1,
        value = FactValueNumeric
    ) |>
    mutate(value = value / 100) |>
    pivot_wider(id_cols = entity_id, names_from = sex, values_from = value) |>
    left_join(
        gdp_per_capita_raw |>
            select(entity_id, gdp_per_capita = value),
        join_by(entity_id)
    ) |>
    left_join(entities, join_by(entity_id)) |>
    select(
        entity_name,
        income_level_name,
        region_name,
        male = Male,
        female = Female,
        gdp_per_capita
    ) |>
    drop_na()

write_csv(fraction, "fractions.csv")
