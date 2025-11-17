use std::collections::HashSet;
use std::fs;
use std::path::Path;
use anyhow::Result;

pub fn build_cache(download_path: &Path) -> Result<HashSet<String>> {
  let mut cache = HashSet::new();

  if !download_path.exists() {
    println!("Download path does not exist: {:?}", download_path);
    return Ok(cache);
  }

  for entry in fs::read_dir(download_path)? {
    let entry = entry?;
    if entry.path().is_file() {
      if let Some(filename) = entry.file_name().to_str() {
        // Extract URI from filename (remove .png extension)
        let uri = filename.strip_suffix(".png")
            .unwrap_or(filename)
            .to_string();
        cache.insert(uri);
      }
    }
  }

  println!("Cache built: {} files indexed", cache.len());
  Ok(cache)
}

pub fn save_cache(cache: &HashSet<String>, cache_path: &Path) -> Result<()> {
  let cache_vec: Vec<&String> = cache.iter().collect();
  let json = serde_json::to_string_pretty(&cache_vec)?;
  fs::write(cache_path, json)?;
  println!("Cache saved to: {:?}", cache_path);
  Ok(())
}

pub fn load_cache(cache_path: &Path) -> Result<HashSet<String>> {
  if !cache_path.exists() {
    return Ok(HashSet::new());
  }
  let contents = fs::read_to_string(cache_path)?;
  let cache_vec: Vec<String> = serde_json::from_str(&contents)?;
  Ok(cache_vec.into_iter().collect())
}