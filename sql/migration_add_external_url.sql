-- migration_add_external_url.sql
ALTER TABLE textures
  ADD COLUMN external_url TEXT NULL AFTER file_path,
  ADD COLUMN source VARCHAR(50) DEFAULT 'external' AFTER external_url;
