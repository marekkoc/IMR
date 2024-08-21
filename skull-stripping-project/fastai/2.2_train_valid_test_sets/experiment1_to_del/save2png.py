all_slices = get_all_slices(evin_disc_mask_fn)
for i in range(len(all_slices)):
    img = Image.fromarray(all_slices[i].astype('uint8'))
    img = img.convert('RGB')
    img.save(f"{output_dir}/{subj_id}_{i}.png")
    #mpl.image.imsave(f"{output_dir}/{subj_id}_{i}.png", all_slices[i], cmap='gray')

    
    
    
#df['usage'] = df['usage'].apply(lambda x: True if x =='val' else False)
#SegmentationItemList.from_df(df,'/').split_from_df(col='usage').label_from_df(cols='seg_path', classes=codes)