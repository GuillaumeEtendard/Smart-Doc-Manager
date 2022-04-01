import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO
import scala.collection.mutable.ListBuffer

object Image{

  def getListOfFiles(dir: String):List[File] = {
    val d = new File(dir)
    if (d.exists && d.isDirectory) {
      d.listFiles.filter(_.isFile).toList
    } else {
      List[File]()
    }
  }

  def fromFolderToByte(path: String): Unit = {
    val files = getListOfFiles(path)
    files.foreach(file =>
      kafkaProducer.sendReport("test",1, message=imageToBytes(ImageIO.read(file)).toString()))
  }

  def imageToBytes(img : BufferedImage): List[List[(Int,Int,Int,Int)]] = {
    val imgHeight = new ListBuffer[List[(Int,Int,Int,Int)]]()
    val imgWidth = new ListBuffer[(Int,Int,Int,Int)]()
    val height = img.getHeight()
    val width = img.getWidth()
    for ( j <- 0 until height) {
      imgWidth.clear()
      for ( i <- 0 until  width) {
        val pixel = b2rgb(img.getRGB(i, j))
        imgWidth += pixel
      }
      imgHeight += imgWidth.toList
    }
    imgHeight.toList
  }

  def b2rgb(b: Int): (Int,Int,Int,Int) = ((b & 0xff000000) >>> 24, (b & 0xff0000) >> 16, (b & 0xff00) >> 8, b & 0xff)

}
