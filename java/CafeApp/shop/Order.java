package shop;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class Order {
	int id;
	Map<Item, Integer> items,offitems;
	Map<Eat, Integer> eat;
	String customer;

	public Order() {
		items = new HashMap<Item, Integer>();
		offitems = new HashMap<Item, Integer>();
		eat = new HashMap<Eat, Integer>();
	}

	public Set<Item> getItems() {
		return items.keySet();
	}

	public Set<Eat> geteatItems() {
		return eat.keySet();
	}

	public Set<Item> getoffItems() {
		return offitems.keySet();
	}

	public int getItemCount(Item item) {
		return items.get(item);
	}

	public int geteatItemCount(Eat item) {
		return eat.get(item);
	}


	public int getoffItemCount(Item item) {
		return offitems.get(item);
	}

	public void add(Item item, int count) {
		if (! items.containsKey(item)) {
			items.put(item, count);
		} else {
			int n = items.get(item);
			if (n + count > 0)
				items.put(item, n + count);
			else
				items.remove(item);
		}
	}

	public void add2(Item item, int count) {
		if (! offitems.containsKey(item)) {
			offitems.put(item, count);
		} else {
			int n = offitems.get(item);
			if (n + count > 0)
				offitems.put(item, n + count);
			else
				offitems.remove(item);
		}
	}

	public void add3(Eat item, int count) {
		if (! eat.containsKey(item)) {
			eat.put(item, count);
		} else {
			int n = eat.get(item);
			if (n + count > 0)
				eat.put(item, n + count);
			else
				eat.remove(item);
		}
	}
	// 自動生成されたgetter/setter

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getCustomer() {
		return customer;
	}

	public void setCustomer(String customer) {
		this.customer = customer;
	}

}
