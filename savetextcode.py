text_list = []
log_t = np.log(t)
log_z = np.log(z)
text_list.append(log_t)
text_list.append(log_z)
np.savetxt("Data", np.transpose(text_list))