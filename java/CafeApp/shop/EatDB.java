package shop;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class EatDB {
	static List<Eat> items = new ArrayList<Eat>();

	static Map<String,Eat> itemIndex = new HashMap<String,Eat>();


	static {
	Eat[] items = { // 商品名に空白は含めない
				new Eat("Chocolatecookies"  ,190), // エスプレッソ Single
				new Eat("Cinnamonroll",270), // エスプレッソ Double
				new Eat("Chiffoncake", 350), // ドリップ アラビカ Small
				new Eat("Cheesecake" ,400), // ドリップ アラビカ Large
				new Eat("Raspberryscone" ,240),// ドリップ ロバスタ Small
				new Eat("Eggsandwich" ,440),
				new Eat("Lasagna" ,480),// ドリップ ロバスタ Middle
				new Eat("Tunasandwich" ,450),// ドリップ ロバスタ Large
				new Eat("Applepie",200), // Java Special
		};
		for(Eat item : items) {
			register(item);
		}


		// 在庫の確保
		InventoryDB inventory = InventoryDB.createInventoryDB();
		for(Eat item : items) {
			inventory.accept(item,10);
		}
	}

	public static void register(Eat item) {
		synchronized(items) {
			int no = items.size();
			item.setId(no);
			items.add(item);

			itemIndex.put(item.getName(), item);
		}
	}


	public static Eat search(int id) {
		synchronized(items) {
			return items.get(id);
		}
	}

	public static Eat search(String name) {
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
