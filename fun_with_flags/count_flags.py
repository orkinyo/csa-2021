class Flag:
    def __init__(self, name, price, description, colors, stripes, stars):
        self.name = name
        self.price = price
        self.description = description
        self.colors = colors
        self.stripes = stripes
        self.stars = stars

    def __str__(self):
        return f'{self.name} - {self.description} (price: {self.price})'

available_flags = [
    Flag("Suriname",    100, "The smallest South American country", 4, 5, 1),
    Flag("Togo",        100, "Has French as the official language", 4, 5, 1),
    Flag("Azerbaijan",  100, "The Land of Fire", 4, 3, 1),
    Flag("Liberia",     200, "Has Africa's cleanest cities", 3, 11, 1),
    Flag("Myanmar",     200, "Formerly known as Burma", 4, 3, 1),
    Flag("Philippines", 300, "Named after King Philip II of Spain", 4, 2, 1),
    Flag("Uzbekistan",  400, "Has the world's largest open-pit gold mine", 4, 5, 12),
    Flag("Tajikistan",  500, "Has the world's second highest dam", 4, 3, 7),
    Flag("Slovenia",    600, "Has the world's longest stone arch railroad bridge", 3, 3, 3),
    Flag("Syria",       700, "Has the world's oldest operational dam", 4, 3, 2),
    Flag("Honduras",    800, "Has a dual capital", 2, 2, 5),
    Flag("Cape Verde",  900, "Named after the Cap-Vert peninsula", 4, 5, 10),
    Flag("Israel",     1000, "The country that brought you CSA", 2, 2, 1),
    Flag("Russia",     1200, "Home to the Hermitage Museum", 3, 3, 0),
    Flag("USA",        1200, "United States of America", 3, 13, 50),
    Flag("Cuba",       1300, "Famous for it's cigars", 3, 5, 1),
    Flag("CSA",        1337, "JustForCheck", 1, 33, 7),
    Flag("Jordan",     1400, "Home to Petra", 4, 3, 1),
    Flag("Singapore",  1400, "The world's second most densely populated country", 2, 2, 5),
    Flag("Venezuela",  1500, "Home to the world's highest waterfall", 4, 3, 8),
]

sum_stars = 0

for flag in available_flags:
    sum_stars += flag.stars
print(f"there are {sum_stars} total stars")