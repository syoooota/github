package shop;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ItemDB {
	static List<Item> items = new ArrayList<Item>();

	static Map<String,Item> itemIndex = new HashMap<String,Item>();


	static {
		Item[] items = { // 商品名に空白は含めない
				new Item("Espresso(S)"  ,100,1), // エスプレッソ Single
				new Item("Espresso(D)",200,1), // エスプレッソ Double
				new Item("Arabica(S)", 300,1), // ドリップ アラビカ Small
				new Item("Arabica(M)" ,400,1), // ドリップ アラビカ Middle
				new Item("Arabica(L)" ,500,2), // ドリップ アラビカ Large
				new Item("Robusta(S)" ,350,1),// ドリップ ロバスタ Small
				new Item("Robusta(M)" ,450,1),// ドリップ ロバスタ Middle
				new Item("Robusta(L)" ,550,2),// ドリップ ロバスタ Large
				new Item("Java(L)",600,3), // Java Special
		};
		for(Item item : items) {
			register(item);
		}


		// 在庫の確保
		InventoryDB inventory = InventoryDB.createInventoryDB();
		for(Item item : items) {
			inventory.accept(item,10);
		}
	}

	public static void register(Item item) {
		synchronized(items) {
			int no = items.size();
			item.setId(no);
			items.add(item);

			itemIndex.put(item.getName(), item);
		}
	}


	public static Item search(int id) {
		synchronized(items) {
			return items.get(id);
		}
	}

	public static Item search(String name) {
		synchronized(items) {
			return itemIndex.get(name);
		}
	}



	public static int getItems() {
		synchronized(items) {
			return items.size();
		}
	}

}
