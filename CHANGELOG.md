# Changelog - xer-reader

## 0.1.3 - 2023-10-06

General code clean up.

---

## 0.1.2 - 2023-10-05

### Added

* Added `currency` attribute pulled from ERMHDR values.  
* Added `get_table_names` method.  
* Added `has_table` method.  
* Added `parse_tables` method. Replaces the `tables` attribute.

### Removed  

* Removed `tables` attribute. The tables are now returned in the `parse_tables` method.

---

## 0.1.1 - 2023-09-30

Fixed typo in README example.

---

## 0.1.0 - 2023-09-30

Initial version.

---