if checkbox1 and checkbox2 and checkbox3 and checkbox4:
    print("All checkboxes are selected")
elif checkbox1 and checkbox2 and checkbox3:
    print("Checkboxes 1, 2, and 3 are selected")
elif checkbox1 and checkbox2 and checkbox4:
    print("Checkboxes 1, 2, and 4 are selected")
elif checkbox1 and checkbox3 and checkbox4:
    print("Checkboxes 1, 3, and 4 are selected")
elif checkbox2 and checkbox3 and checkbox4:
    print("Checkboxes 2, 3, and 4 are selected")
elif checkbox1 and checkbox2:
    print("Checkboxes 1 and 2 are selected")
elif checkbox1 and checkbox3:
    print("Checkboxes 1 and 3 are selected")
elif checkbox1 and checkbox4:
    print("Checkboxes 1 and 4 are selected")
elif checkbox2 and checkbox3:
    print("Checkboxes 2 and 3 are selected")
elif checkbox2 and checkbox4:
    print("Checkboxes 2 and 4 are selected")
elif checkbox3 and checkbox4:
    print("Checkboxes 3 and 4 are selected")
elif checkbox1:
    print("Checkbox 1 is selected")
elif checkbox2:
    print("Checkbox 2 is selected")
elif checkbox3:
    print("Checkbox 3 is selected")
elif checkbox4:
    print("Checkbox 4 is selected")
else:
    print("No checkboxes are selected")
