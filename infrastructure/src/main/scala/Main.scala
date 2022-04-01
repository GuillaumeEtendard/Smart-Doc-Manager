import org.apache.log4j.{Level, Logger}

object Main{
  def main(args: Array[String]): Unit = {
    Logger.getLogger("org").setLevel(Level.OFF)
    Logger.getLogger("akka").setLevel(Level.OFF)
    Image.fromFolderToByte("images/")
    kafkaConsumer.consumeAll()
  }
}
