package shop;

public class Item {
	int id; // 商品コード
	String name ; // 商品名

	int price,time; // 価格


	public int getTime() {
		return time;
	}

	public void setTime(int time) {
		this.time = time;
	}

	public Item(String name, int price,int time) {
		this.name = name;
		this.price = price;
		this.time=time;

	}

	// 以下はEclipseの「getterおよびsetterの生成」により自動生成

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getPrice() {
		return price;
	}

	public void setPrice(int price) {
		this.price = price;
	}

	// 以下はEclipseの「hashCodeおよびequalsの生成」により自動生成

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + id;
		result = prime * result + ((name == null) ? 0 : name.hashCode());
		result = prime * result + price;
		result = prime * result + time;
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Item other = (Item) obj;
		if (id != other.id)
			return false;
		if (name == null) {
			if (other.name != null)
				return false;
		} else if (!name.equals(other.name))
			return false;
		if (price != other.price)
			return false;
		if (time != other.time)
			return false;
		return true;
	}

}
