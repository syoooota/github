package kadai;

import java.awt.Graphics;
import java.awt.Image;

@SuppressWarnings("serial")
public class Shoot2 extends Shoot {

	// double buffering
	Image buffer;

	public void init() {
		super.init();
		buffer = createImage(getWidth(), getHeight());
	}

	public void paint(Graphics g) {

		g.drawImage(buffer, 0, 0, this);
	}

	@Override
	public void repaint() {
		super.paint(buffer.getGraphics());
		super.repaint();

	}

	public void update(Graphics g) {
		paint(g);
	}

}