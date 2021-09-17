#include "shopping_cart.h"

struct shopping_cart shopping_cart;
char user_input[STRING_BUFFER_SIZE];
bool loaded_coupons;

int get_free_index() {
	for (int i = 0; i < SHOPPING_CART_SIZE; i++) {
		if (shopping_cart.items[i].type == TYPE_UNDEFINED) {
			return i;
		}
	}
	return -1;
}

item* add_item(enum item_type type) {
	int idx = get_free_index();
	if (idx == -1) {
		printf("Can't add more items to your shopping cart!\n");
		exit(0);
	}
	shopping_cart.items[idx].type = type;
	shopping_cart.amount_of_items++;
	return &shopping_cart.items[idx];
}

void remove_item(int index) {
	if (shopping_cart.items[index].type == TYPE_UNDEFINED) {
		printf("Item %d is not in your shopping cart!\n", index);
		return;
	}
	shopping_cart.items[index].type = TYPE_UNDEFINED;
	shopping_cart.amount_of_items--;
	printf("Item %d removed!\n", index);
}

bool can_edit_item(item* item){
	if ((item->type == TYPE_UNDEFINED)) {
		printf("There is no item at selected index\n");
		return false;
	} else if 
		(((item->type == TYPE_BREAD) && (item->grocery_item.amount_loaves > 0)) || ((item->type == TYPE_PASTA) && (item->grocery_item.amount_kilograms > 0)) ||
		((item->type == TYPE_SOUP) && (item->grocery_item.amount_liters > 0)) || ((item->type == TYPE_DRINK) && (item->grocery_item.amount_liters > 0)) ||
		((item->type == TYPE_VEGETABLE) && (item->grocery_item.amount_kilograms > 0)) || ((item->type = TYPE_FRUIT) && (item->grocery_item.amount_items > 0))) {
		return true;
	} else if ((item->type = TYPE_COUPON)) {
		printf("Item is a coupon!\n");
		return false;
	} else {
		printf("Invalid item type!\n");
		return false;
	}
}

bool is_valid_food_type(enum item_type type) {
	return (
		(type == TYPE_BREAD)     || 
		(type == TYPE_PASTA)     || 
		(type == TYPE_SOUP)      || 
		(type == TYPE_DRINK)     || 
		(type == TYPE_VEGETABLE) || 
		(type == TYPE_FRUIT));
}

char* food_type_to_unit(enum item_type type) {
	switch (type) {
		case TYPE_BREAD:
			return "loaves";
			break;
		case TYPE_PASTA:
		case TYPE_VEGETABLE:
			return "kilogram(s)";
			break;
		case TYPE_SOUP:
		case TYPE_DRINK:
			return "liter(s)";
			break;
		case TYPE_FRUIT:
			return "unit(s)";
			break;
	}
}

bool is_coupon_valid(char* coupon) {
	// black list of expired coupons
	if (!memcmp(coupon, "NOT_A_FLAG{I_L0V3_CSA}", strlen(coupon)) ||
		!memcmp(coupon, "NOT_A_FLAG{G1V3_M3_M0R3_C0UP0N5_PL3453}", strlen(coupon)) ||
		!memcmp(coupon, "NOT_A_FLAG{TH3_C4K3_1S_A_L1E}", strlen(coupon))) {
		return false;
	} else {
		return true;
	}
}

void load_coupon(char* path, int discount) {
	char coupon[STRING_BUFFER_SIZE];

	FILE *fp = fopen(path, "r");
	if (fp == NULL) {
		printf("Unable to open file! (%s)\n", path);
		exit(0);
	}

	if (fgets(coupon, STRING_BUFFER_SIZE, fp) == NULL) {
		printf("Could not load coupon %s!\n", path);
		exit(0);
	}
	fclose(fp);

	int is_valid = is_coupon_valid(coupon);
	if (!is_valid) {
		return;
	}

	item* item = add_item(TYPE_COUPON);
	item->coupon.discount_amount = discount;
	item->coupon.have_entered = false;
	item->coupon.is_valid = is_valid;
	item->coupon.length = strlen(coupon);
	item->coupon.expiration_day = 0;  // todo - implement expiration date check
	item->coupon.expiration_month = 0;
	item->coupon.expiration_year = 0;
	strncpy(item->coupon.code, coupon, strlen(coupon));
}
