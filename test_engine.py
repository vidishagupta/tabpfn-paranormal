"""Verification test script for TabPFN Paranormal Engine"""
import pandas as pd
from paranormal_engine import TabPFNParanormalDetector
from dossier_generator import DossierGenerator

def main():
    print("Testing TabPFN Paranormal Engine...")
    detector = TabPFNParanormalDetector()
    generator = DossierGenerator()

    # Test Blackwood Manor
    df = pd.read_csv("demo_datasets/blackwood_manor_3am.csv")
    results = detector.analyze(df)

    print(f"Dataset Rows: {len(results['processed_df'])}")
    print(f"Peak Anomaly Score: {results['peak_score']}%")
    print(f"Threat Level: {results['threat_level']}")
    print(f"Peak Time: {results['peak_timestamp']}")
    print("Classification Probabilities:")
    for k, v in results['classification_probs'].items():
        print(f"  - {k}: {v}%")

    assert results["peak_score"] > 70, "Blackwood Manor should trigger a critical anomaly score!"
    assert "processed_df" in results

    print("\nTesting Dossier Generation...")
    dossier = generator.generate_dossier(results, "Test manual field observation.")
    assert len(dossier) > 200, "Dossier should be substantive!"
    print(f"Generated Dossier Length: {len(dossier)} characters")
    print("SUCCESS: Engine and Dossier pipeline verified!")

if __name__ == "__main__":
    main()
