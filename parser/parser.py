import os
import camelot
import logging
import fitz # PyMuPDF


# camelotLogger = logging.getLogger("camelot")
# camelotLogger.setLevel(logging.ERROR)

logger = logging.Logger("codniv-parser")
logger.setLevel(logging.INFO)

format_string = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(format_string, datefmt="%Y-%m-%dT%H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)


class ConversionBackend(object):
    def convert(self, pdf_path, png_path, resolution=300):
        doc = fitz.open(pdf_path)

        print(f"pdf_path: {pdf_path}, png_path: {png_path}")

        pix = doc[0].get_pixmap(dpi=resolution)
        pix.save(png_path)


kwargs = {
    "pages": "all",
    "suppress_stdout": False,
    # Don't make this very large or else text gets recognized as lines
    "line_scale": 25,
    "backend": ConversionBackend(),
}

# Create csvs directory if it doesn't exist
if not os.path.exists("csvs"):
    logger.debug("Creating csvs directory")
    os.makedirs("csvs")
else:
    logger.debug("csvs exists, now checking if it is a directory")
    if not os.path.isdir("csvs"):
        raise Exception("csvs is not a directory")


def get_tables(pdf):
    filtered_tables = []
    for table in pdf:
        # Got it from experimenting
        if (table.accuracy < 70) or (table.whitespace > 65 and table.accuracy < 90):
            logger.debug(
                f"Table accuracy: {table.accuracy}, whitespace: {table.whitespace}"
            )
            continue
        filtered_tables.append(table)

    return filtered_tables


def parse_pdf(pdf_path, password=None):
    tables = []
    try:
        # TODO:
        # Optimizing can be done here, alot of file read and write operations can be eliminated
        # A large file can be broken into smaller chunks and then process simultaneously using threading
        # cause internally it processes page by page
        # Need to rewrite just the file operations, rest seems to align with the requirements

        pdf = camelot.read_pdf(
            pdf_path,
            password=password,
            **kwargs,
        )
    except Exception as e:
        logger.error("Corrupted PDF")
        logger.error(e)
        return tables

    filtered_tables = get_tables(pdf)

    logger.info(f"Total tables detected: {len(pdf)}")
    logger.info(f"True tables detected: {len(filtered_tables)}")
    logger.info(f"False positive tables: {len(pdf) - len(filtered_tables)}")

    if len(filtered_tables) == 0:
        logger.warning("No tables detected")

    for index, table in enumerate(filtered_tables):
        base_pdf_name = os.path.basename(pdf_path)
        csv_file_name = base_pdf_name.replace(".pdf", f"-table-{index}.csv")

        csv_save_path = f"csvs/{csv_file_name}"

        logger.info(f"Basename: {base_pdf_name}, CSV file name: {csv_file_name}")

        table.to_csv(f"{csv_save_path}")
        logger.info(f"Saved table to csv {csv_save_path}")

        tables.append({"csv_path": csv_save_path, "table": table})

    return tables
