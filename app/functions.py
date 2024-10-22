

# function to calculate letter grade based on number grade
def calculate_grade (number_grade):
    if number_grade >= 90:
        letter_grade = "A"
    elif number_grade >= 80:
        letter_grade = "B"
    elif number_grade >= 70:
        letter_grade = "C"
    elif number_grade >= 60:
        letter_grade = "D"
    else:
        letter_grade = "F"
    return letter_grade


#test the function
print(calculate_grade(85)) #should return B

#create function that calculates loan amortization monthly payment
def loan_amortization_calculation(loan_amount, term_years, interest_rate):
    term_months = term_years * 12
    monthly_interest_rate = interest_rate / 100 / 12
    monthly_payment = loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -term_months)
    return monthly_payment

#test the function
print(loan_amortization_calculation(1000, 2, 5)) #should return 43.87