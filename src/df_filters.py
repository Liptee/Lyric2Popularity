import re
import json
import pandas as pd
from typing import List
from src.lyrics_similarity import lyrics_similarity
from tqdm import tqdm


class DFFilters():
    @staticmethod
    def popularity(df: pd.DataFrame,
                k: int,
                more_than: bool = True) -> pd.DataFrame:
        if more_than: return df[df["popularity"] > k]
        else: return df[df["popularity"] < k]

    @staticmethod
    def language(df: pd.DataFrame,
                mapping_file: str,
                white_list: List[str]=None,
                black_list: List[str]=None) -> pd.DataFrame:
        if white_list and black_list:
            raise ValueError("Only one of white_list or black_list can be provided")
        if not white_list and not black_list:
            raise ValueError("One of white_list or black_list must be provided")
        
        with open(mapping_file, encoding="utf-8") as f:
            mapping = json.load(f)
            if white_list:
                mapping = {k: [song_id.split(".json")[0] for song_id in v] for k, v in mapping.items() if k in white_list}
            elif black_list:
                mapping = {k: [song_id.split(".json")[0] for song_id in v] for k, v in mapping.items() if k not in black_list}

        files_to_keep = []
        for lang in mapping.keys():
            files_to_keep.extend(mapping[lang])

        df = df[df["track_id"].isin(files_to_keep)]
        return df

    @staticmethod
    def release_date(df: pd.DataFrame,
                    start_year: int = 1900,
                    end_year: int = 2030) -> pd.DataFrame:
        # in df release_date is in format "YYYY-MM-DD" or "YYYY" or "YYYY-MM"
        df = df[df["release_date"].notna()].copy()

        # strip release_date to format "YYYY"
        def strip_release_date(date: str) -> int:
            return int(date[:4])

        df["year"] = df["release_date"].apply(strip_release_date)
        df = df[df["year"] >= start_year]
        df = df[df["year"] <= end_year]
        # delete year column
        df = df.drop(columns=["year"])
        return df

    @staticmethod   
    def live(df: pd.DataFrame) -> pd.DataFrame:
        LIVE_TAGS = [
        r'[-–]\s*live\b',             # «- live»
        r'\( *live\b',                # «(live»
        r'\blive\s+(at|from|in|on|aid|and|&)\b',
        r'\blive/\d{2,4}',            # «live/2011»
        r'\brecorded +live\b',        # «recorded live»
        
        ]
        LIVE_REGEX = re.compile('|'.join(LIVE_TAGS), re.I)

        df["track_name"] = df["track_name"].str.lower()
        df["is_live"] = df["track_name"].str.contains(LIVE_REGEX)
        df = df[df["is_live"] == False]
        df = df.drop(columns=["is_live"])
        return df

    @staticmethod
    def acoustic(df: pd.DataFrame) -> pd.DataFrame:
        ACOUSTIC_TAGS = [
        r'[-–]\s*acoustic\b',        # «- acoustic»
        r'\( *acoustic\b',           # «(acoustic»
        r'\bacoustic +version\b',    # «acoustic version»
        r'\bacoustic +mix\b',        # «acoustic mix»
        r'\bacoustic +take\b',       # «acoustic take 2» и т.п.
        ]
        ACOUSTIC_REGEX = re.compile('|'.join(ACOUSTIC_TAGS), re.I)

        df["track_name"] = df["track_name"].str.lower()
        df["is_acoustic"] = df["track_name"].str.contains(ACOUSTIC_REGEX)
        df = df[df["is_acoustic"] == False]
        df = df.drop(columns=["is_acoustic"])
        return df

    @staticmethod
    def remix(df: pd.DataFrame) -> pd.DataFrame:
        df["track_name"] = df["track_name"].str.lower()
        df["is_remix"] = df["track_name"].str.contains(r"remix", case=False)
        df = df[df["is_remix"] == False]
        df = df.drop(columns=["is_remix"])
        return df

    @staticmethod
    def cover(df: pd.DataFrame) -> pd.DataFrame:
        COVER_TAGS = [
        r'[-–]\s*cover\b',            # «… - Cover»
        r'\bcover\s+version\b',       # «cover version»
        r'\bcover\s+by\b',            # «cover by …»
        r'\(.*\bcover\b.*\)',         # «(… Cover …)»
        ]
        COVER_RX = re.compile('|'.join(COVER_TAGS), re.I)

        df["track_name"] = df["track_name"].str.lower()
        df["is_cover"] = df["track_name"].str.contains(COVER_RX)
        df = df[df["is_cover"] == False]
        df = df.drop(columns=["is_cover"])
        return df

    @staticmethod
    def smart_cover(
            df: pd.DataFrame,
            sim_threshold: float = 0.60,
            verbose: bool = False
    ) -> pd.DataFrame:
        """
        Считаем кавером трек с тем же именем и ≽ sim_threshold совпадением lyrics;
        оставляем запись с самым ранним release_date (или без неё, если других нет).
        """
        def safe_year(date):
            try:
                return int(str(date)[:4])
            except Exception:
                return 9999

        df = df.copy()
        df["track_name_norm"] = df["track_name"].str.lower().str.strip()

        # если одна и та же песня (track_id) дублируется, оставим только первую запись
        df = df.drop_duplicates(subset="track_id", keep="first")

        keep_idx = []

        for _, grp in tqdm(df.groupby("track_name_norm"), desc="Smart cover"):
            grp = (grp
                .assign(_year=grp["release_date"].apply(safe_year))
                .sort_values("_year")
                .drop(columns="_year"))

            originals: list[tuple[str, int]] = []   # [(lyrics, idx)]

            for idx, row in grp.iterrows():
                lyrics = row.get("lyrics") or ""
                is_cover = False

                if lyrics:
                    for lyr_orig, idx_orig in originals:
                        if lyrics_similarity(lyrics, lyr_orig) >= sim_threshold:
                            orig_row = df.loc[idx_orig]
                            if verbose:
                                print(f"Original: {orig_row['track_name']} / {orig_row['track_artist']}  id:{orig_row['track_id']}")
                                print(f"Cover   : {row['track_name']} / {row['track_artist']}  id:{row['track_id']}")
                                print("Sim     :", lyrics_similarity(lyrics, lyr_orig))
                                print("-" * 32)
                            is_cover = True
                            break

                if not is_cover:
                    originals.append((lyrics, idx))
                    keep_idx.append(idx)

        return df.loc[keep_idx].drop(columns=["track_name_norm"])
