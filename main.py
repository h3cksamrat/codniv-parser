import camelot


# Works for good table like page3, page4
# Bugs out on page1 where the table is not present
# pdf2 some of the table are not detected
for i in range(1, 6):
    try:
        pdf = camelot.read_pdf(
            f"pdfs/pdf{i}.pdf",
            pages="all",
            # for table with border lines in background
            process_background=True,
        )

        print("=====================================")
        print(f"pdf{i}.pdf")
        for table in pdf:
            print(table.df)
    except Exception as e:
        print(f"Error in pdf{i}.pdf")
        print(e)
    finally:
        print("=====================================")

# Possible solution for page1 is to use table_areas parameter
# Have guard rails that checks if the table is detected or not
# If detected, then use table_areas parameter with layout='stream'
