#ifndef SHOPPING_CART_H
#define SHOPPING_CART_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define SHOPPING_CART_SIZE 100
#define STRING_BUFFER_SIZE 100
#define HIGH_DISCOUNT_AMOUNT 90


enum item_type {
	TYPE_UNDEFINED = 0,
	TYPE_BREAD     = 'b', // loaves
	TYPE_PASTA     = 'p', // kilograms
	TYPE_SOUP      = 's', // liters
	TYPE_DRINK     = 'd', // liters
	TYPE_VEGETABLE = 'v', // kilograms
	TYPE_FRUIT     = 'f', // items
	TYPE_COUPON    = 'c',
};

struct coupon_item {
	int discount_amount;
	int have_entered;
	int is_valid;
	int length;
	int expiration_day;
	int expiration_month;
	int expiration_year;
	char code[STRING_BUFFER_SIZE];
};

struct grocery_item {
	int amount_grams; // deprecated - use kilograms instead
	int amount_kilograms;
	int amount_items;
	int amount_loaves;
	int amount_liters;
	char description[STRING_BUFFER_SIZE];
};

struct shopping_cart_item {
	enum item_type type;
	union {
		struct coupon_item coupon;
		struct grocery_item grocery_item;
	};
};
typedef struct shopping_cart_item item;


struct shopping_cart {
	int amount_of_items;
	item items[SHOPPING_CART_SIZE];
};


item* add_item(enum item_type type);
void remove_item(int index);
bool can_edit_item(item* item);
bool is_valid_food_type(enum item_type type);
char* food_type_to_unit(enum item_type type);
void load_coupon(char* path, int discount);


#endif /* SHOPPING_CART_H */
