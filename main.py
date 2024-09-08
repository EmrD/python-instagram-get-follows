import customtkinter as ctk
import requests

def get_all_followers(user_id, cookie):
    base_url = f"https://i.instagram.com/api/v1/friendships/{user_id}/followers/"
    params = {'count': 12}
    followers = []

    while True:
        response = requests.get(
            base_url,
            params=params,
            headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)',
                'Cookie': cookie
            }
        )
        data = response.json()

        if not data.get('users'):
            break

        followers.extend(data['users'])

        if 'next_max_id' in data:
            params['max_id'] = data['next_max_id']
        else:
            break

    return followers

def get_all_following(user_id, cookie):
    base_url = f"https://i.instagram.com/api/v1/friendships/{user_id}/following/"
    params = {'count': 12}
    following = []

    while True:
        response = requests.get(
            base_url,
            params=params,
            headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)',
                'Cookie': cookie
            }
        )
        data = response.json()

        if not data.get('users'):
            break

        following.extend(data['users'])

        if 'next_max_id' in data:
            params['max_id'] = data['next_max_id']
        else:
            break

    return following

def find_non_followers(followers, following):
    follower_usernames = {user['username'] for user in followers}
    non_followers = [user['username'] for user in following if user['username'] not in follower_usernames]
    return non_followers

def update_data():
    global followers_list, following_list, non_followers
    followers_list = get_all_followers(user_id, cookie)
    following_list = get_all_following(user_id, cookie)
    non_followers = find_non_followers(followers_list, following_list)
    
    update_listboxes()

def update_listboxes():
    followers_textbox.configure(state="normal")
    following_textbox.configure(state="normal")
    non_followers_textbox.configure(state="normal")
    
    followers_textbox.delete("1.0", "end")
    for user in followers_list:
        followers_textbox.insert("end", user['username'] + "\n")
    followers_count_label.configure(text=f"Count: {len(followers_list)}")
        
    following_textbox.delete("1.0", "end")
    for user in following_list:
        following_textbox.insert("end", user['username'] + "\n")
    following_count_label.configure(text=f"Count: {len(following_list)}")
        
    non_followers_textbox.delete("1.0", "end")
    for user in non_followers:
        non_followers_textbox.insert("end", user + "\n")
    non_followers_count_label.configure(text=f"Count: {len(non_followers)}")
    
    followers_textbox.configure(state="disabled")
    following_textbox.configure(state="disabled")
    non_followers_textbox.configure(state="disabled")

user_id = '' # paste your user id
cookie = '' # paste your cookie

app = ctk.CTk()
app.geometry("800x600")
app.title("Instagram Follow List")
app.resizable(False, False)

followers_label = ctk.CTkLabel(app, text="Followers", width=250)
followers_label.grid(row=0, column=0, padx=10, pady=10)

followers_textbox = ctk.CTkTextbox(app, width=250, height=300)
followers_textbox.configure(state="disabled")
followers_textbox.grid(row=1, column=0, padx=10, pady=10)
followers_count_label = ctk.CTkLabel(app, text="Count: 0", width=250)
followers_count_label.grid(row=2, column=0, padx=10, pady=10)

following_label = ctk.CTkLabel(app, text="Following", width=250)
following_label.grid(row=0, column=1, padx=10, pady=10)

following_textbox = ctk.CTkTextbox(app, width=250, height=300)
following_textbox.configure(state="disabled")
following_textbox.grid(row=1, column=1, padx=10, pady=10)
following_count_label = ctk.CTkLabel(app, text="Count: 0", width=250)
following_count_label.grid(row=2, column=1, padx=10, pady=10)

non_followers_label = ctk.CTkLabel(app, text="Non Followers", width=250)
non_followers_label.grid(row=0, column=2, padx=10, pady=10)

non_followers_textbox = ctk.CTkTextbox(app, width=250, height=300)
non_followers_textbox.configure(state="disabled")
non_followers_textbox.grid(row=1, column=2, padx=10, pady=10)
non_followers_count_label = ctk.CTkLabel(app, text="Count: 0", width=250)
non_followers_count_label.grid(row=2, column=2, padx=10, pady=10)

update_button = ctk.CTkButton(app, text="Update Data", command=update_data)
update_button.grid(row=3, column=0, columnspan=3, pady=10)

app.mainloop()
