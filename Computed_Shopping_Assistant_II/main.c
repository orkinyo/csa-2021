#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include "shopping_cart.h"

extern struct shopping_cart shopping_cart;
extern char user_input[];
extern bool loaded_coupons;

void add_item_menu() {
	printf("Which item would you like to add?\n");
	printf("%c - Bread\n", TYPE_BREAD);
	printf("%c - Pasta\n", TYPE_PASTA);
	printf("%c - Soup\n", TYPE_SOUP);
	printf("%c - Drink\n", TYPE_DRINK);
	printf("%c - Vegetable\n", TYPE_VEGETABLE);
	printf("%c - Fruit\n", TYPE_FRUIT);

	char choice_type;
	scanf(" %c", &choice_type);

	if (!is_valid_food_type(choice_type)) {
		printf("Invalid type entered!\n");
		return;
	}

	item* item = add_item(choice_type);

	switch (choice_type) {
		case TYPE_BREAD:
			strcpy(item->grocery_item.description, "White bread");
			item->grocery_item.amount_loaves = 1;
			break;
		case TYPE_PASTA:
			strcpy(item->grocery_item.description, "Spaghetti");
			item->grocery_item.amount_kilograms = 1;
			break;
		case TYPE_SOUP:
			strcpy(item->grocery_item.description, "Lentil soup");
			item->grocery_item.amount_liters = 1;
			break;
		case TYPE_DRINK:
			strcpy(item->grocery_item.description, "Coca-Cola");
			item->grocery_item.amount_liters = 1;
			break;
		case TYPE_VEGETABLE:
			strcpy(item->grocery_item.description, "Potatoes");
			item->grocery_item.amount_kilograms = 1;
			break;
		case TYPE_FRUIT:
			strcpy(item->grocery_item.description, "Apples");
			item->grocery_item.amount_items = 1;
			break;
	}
	printf("1 %s of %s added!\n", food_type_to_unit(choice_type), item->grocery_item.description);
}

void edit_item_menu() {
	if (shopping_cart.amount_of_items == 0) {
		printf("Your shopping cart is empty!\n");
		return;
	}
	printf("Which item index would you like to edit?\n");

	int choice;
	scanf("%d", &choice);
	if (choice < 0 || choice >= SHOPPING_CART_SIZE) {
		printf("Invalid item index!\n");
		return;
	}
	item* item = &shopping_cart.items[choice];

	if (!can_edit_item(item)) {
		printf("Can not edit this item!\n");
		return;
	}

	printf("Which property would you like to edit?\n"
		"1 - Type\n"
		"2 - Amount of kilograms\n"
		"3 - Amount of items\n"
		"4 - Amount of loaves\n"
		"5 - Amount of liters\n"
		"6 - Description\n"
		"7 - Cancel\n");
	scanf("%d", &choice);

	if (choice < 1 || choice > 7) {
		printf("Invalid choice!\n");
		return;
	}

	char newline;
	scanf("%c", &newline); // clear newline from buffer
	char choice_type;

	switch (choice) {
		case 1:
			printf("Enter new type: ");
			fflush(stdout);
			scanf(" %c", &choice_type);
			if (choice_type == TYPE_COUPON) {
				printf("You can not convert to coupon!\n");
			} else if (is_valid_food_type(choice_type)) {
				item->type = choice_type;
			} else {
				printf("Invalid type entered!\n");
			}
			break;
		case 2:
			printf("Enter new kilograms amount: ");
			fflush(stdout);
			scanf("%d", &choice);
			item->grocery_item.amount_kilograms = choice;
			break;
		case 3:
			printf("Enter new items amount: ");
			fflush(stdout);
			scanf("%d", &choice);
			item->grocery_item.amount_items = choice;
			break;
		case 4:
			printf("Enter new loaves amount: ");
			fflush(stdout);
			scanf("%d", &choice);
			item->grocery_item.amount_loaves = choice;
			break;
		case 5:
			printf("Enter new liters amount: ");
			fflush(stdout);
			scanf("%d", &choice);
			item->grocery_item.amount_liters = choice;
			break;
		case 6:
			printf("Enter new description: ");
			fflush(stdout);
			fgets(item->grocery_item.description, STRING_BUFFER_SIZE, stdin);
			item->grocery_item.description[strlen(item->grocery_item.description)-1] = '\0'; // remove newline
			break;
		case 7:
			return;
			break;
	}
	printf("Item updated!\n");
}

void remove_item_menu() {
	if (shopping_cart.amount_of_items == 0) {
		printf("Your shopping cart is empty!\n");
		return;
	}
	printf("Which item index would you like to remove?\n");

	int choice;
	scanf("%d", &choice);
	if (choice < 0 || choice >= SHOPPING_CART_SIZE) {
		printf("Invalid item index!\n");
		return;
	}
	remove_item(choice);
}

void print_shopping_cart() {
	if (shopping_cart.amount_of_items == 0) {
		printf("\nYour shopping cart is empty!\n");
		return;
	}
	printf("\nYour shopping cart has %d items:\n", shopping_cart.amount_of_items);
	for (int i = 0; i < SHOPPING_CART_SIZE; i++) {
		item* item = &shopping_cart.items[i];

		int amount = 0;
		switch (item->type) {
			case TYPE_UNDEFINED:
				break;
			case TYPE_COUPON:
				if (item->coupon.have_entered) {
					if (item->coupon.discount_amount < HIGH_DISCOUNT_AMOUNT) {
						printf("(index %d) - %d%% OFF coupon - %s\n", i, item->coupon.discount_amount, item->coupon.code);
					} else { // need to be a little more discrete about special coupons
						printf("(index %d) - %d%% OFF coupon - *CENSORED*\n", i, item->coupon.discount_amount);
					}
				}
				break;
			default:
				switch (item->type) {
					case TYPE_BREAD:
						amount = item->grocery_item.amount_loaves;
						break;
					case TYPE_PASTA:
					case TYPE_VEGETABLE:
						amount = item->grocery_item.amount_kilograms;
						break;
					case TYPE_SOUP:
					case TYPE_DRINK:
						amount = item->grocery_item.amount_liters;
						break;
					case TYPE_FRUIT:
						amount = item->grocery_item.amount_items;
				}
				printf("(index %d) - %d %s of %s\n", i, amount, food_type_to_unit(item->type), item->grocery_item.description);
				break;
		}
	}
}

void apply_a_coupon() {
	if (!loaded_coupons) {
		load_coupon("coupon_10.txt", 10);
		load_coupon("coupon_50.txt", 50);
		load_coupon("coupon_100.txt", 100);
		loaded_coupons = true;
	}
	printf("Please enter your coupon:\n");
	char newline;
	scanf("%c", &newline); // clear newline from buffer
	fgets(user_input, STRING_BUFFER_SIZE, stdin);
	
	for (int i = 0; i < SHOPPING_CART_SIZE; i++) {
		item* item = &shopping_cart.items[i];
		if (item->type == TYPE_COUPON && !item->coupon.have_entered) {
			if (!memcmp(item->coupon.code, user_input, item->coupon.length)) {
				printf("Applied coupon for %d%% OFF!\n", item->coupon.discount_amount);
				item->coupon.have_entered = true;
				return;
			}
		}
	}
	printf("Invalid coupon!\n");
}

void checkout() {
	printf("\nThank you for choosing Computed Shopping Assistant II !\n");
	printf("Your items will be delivered to you within 24 hours.\n");
	printf("Goodbye!\n");
	exit(0);
}

void main_menu() {
	printf("\n---> Welcome to Computed Shopping Assistant II <---\n");

	while (true) {
		printf("\nWhat would you like to do?\n"
				"1 - Add item to shopping cart\n"
				"2 - Edit item in shopping cart\n"
				"3 - Remove item from shopping cart\n"
				"4 - View shopping cart\n"
				"5 - Apply a coupon\n"
				"6 - Checkout\n");

		int choice = 0;
		scanf("%d", &choice);

		switch (choice) {
			case 1:
				add_item_menu();
				break;
			case 2:
				edit_item_menu();
				break;
			case 3:
				remove_item_menu();
				break;
			case 4:
				print_shopping_cart();
				break;
			case 5:
				apply_a_coupon();
				break;
			case 6:
				checkout();
				break;
			default:
				printf("Invalid choice!\n");
				exit(0);
				break;
		}
	}
}

int main() {
	memset(&shopping_cart, 0, sizeof(shopping_cart));
	main_menu();
}
