package shop;

import java.util.HashMap;
import java.util.Map;

// ItemDBではクラス自身をDBに見立てた。
// ここではSingletonというデザインパターンを使う。
// Singletonは唯一のインスタンス
public class InventoryDB {
	private Map<Item, Integer> stocks;
	private Map<Eat, Integer> stocks2;

	// 通常のコンストラクタは使えないようにする。
	private InventoryDB() {
		stocks = new HashMap<Item, Integer>();
		stocks2 = new HashMap<Eat, Integer>();
	}

	private static InventoryDB db = null;

	public static InventoryDB createInventoryDB() {
		if (db == null) {
			db = new InventoryDB();
		}
		return db;
	}

	public void accept(Item item, int count) {
		if (stocks.containsKey(item)) {
			int n = stocks.get(item);
			stocks.put(item, n + count);
		} else
			stocks.put(item, count);
	}

	public void accept(Eat item, int count) {
		if (stocks2.containsKey(item)) {
			int n = stocks2.get(item);
			stocks2.put(item, n + count);
		} else
			stocks2.put(item, count);
	}

	public void receive(Order order) {
		for (Item item : order.getItems()) {
			accept(item, order.getItemCount(item));
		}
	}

	public void receive2(Order order) {
		for (Eat item : order.geteatItems()) {
			accept(item, order.geteatItemCount(item));
		}
	}

	public void receive3(Order order) {
		for (Item item : order.getoffItems()) {
			accept(item, order.getoffItemCount(item));
		}
	}

	public void ship(Order order) {
		for (Item item : order.getItems()) {
			accept(item, -order.getItemCount(item));
		}
	}

	public void ship2(Order order) {
		for (Eat item : order.geteatItems()) {
			accept(item, -order.geteatItemCount(item));
		}
	}

	public void ship3(Order order) {
		for (Item item : order.getoffItems()) {
			accept(item, -order.getoffItemCount(item));
		}
	}

	public boolean canShip(Order order) {
		for (Item item : order.getItems()) {
			if (getStockCount(item) < order.getItemCount(item))
				return false;
		}
		return true;
	}

	public boolean canShip2(Order order) {
		for (Eat item : order.geteatItems()) {
			if (getStock2Count(item) < order.geteatItemCount(item))
				return false;
		}
		return true;
	}

	public boolean canShip3(Order order) {
		for (Item item : order.getoffItems()) {
			if (getStockCount(item) < order.getoffItemCount(item))
				return false;
		}
		return true;
	}

	public int getStockCount(Item item) {
		if (stocks.containsKey(item))
			return stocks.get(item);
		return 0;
	}

	public int getStock2Count(Eat item) {
		if (stocks2.containsKey(item))
			return stocks2.get(item);
		return 0;
	}
}
